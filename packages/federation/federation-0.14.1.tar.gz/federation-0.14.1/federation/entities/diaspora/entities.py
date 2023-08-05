from lxml import etree

from federation.entities.base import Comment, Post, Reaction, Relationship, Profile, Retraction, BaseEntity, Follow
from federation.entities.diaspora.utils import format_dt, struct_to_xml, get_base_attributes, add_element_to_doc
from federation.exceptions import SignatureVerificationError
from federation.protocols.diaspora.signatures import verify_relayable_signature, create_relayable_signature
from federation.utils.diaspora import retrieve_and_parse_profile


class DiasporaEntityMixin(BaseEntity):
    # Normally outbound document is generated from entity. Store one here if at some point we already have a doc
    outbound_doc = None

    def to_xml(self):
        """Override in subclasses."""
        raise NotImplementedError

    @classmethod
    def from_base(cls, entity):
        return cls(**get_base_attributes(entity))

    @staticmethod
    def fill_extra_attributes(attributes):
        """Implement in subclasses to fill extra attributes when an XML is transformed to an object.

        This is called just before initializing the entity.

        Args:
            attributes (dict) - Already transformed attributes that will be passed to entity create.

        Returns:
            Must return the attributes dictionary, possibly with changed or additional values.
        """
        return attributes


class DiasporaRelayableMixin(DiasporaEntityMixin):
    _xml_tags = []
    parent_signature = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._required += ["signature"]

    def _validate_signatures(self):
        super()._validate_signatures()
        if not self._sender_key:
            raise SignatureVerificationError("Cannot verify entity signature - no sender key available")
        source_doc = etree.fromstring(self._source_object)
        if not verify_relayable_signature(self._sender_key, source_doc, self.signature):
            raise SignatureVerificationError("Signature verification failed.")

    def sign(self, private_key):
        self.signature = create_relayable_signature(private_key, self.to_xml())

    def sign_with_parent(self, private_key):
        if self._source_object:
            doc = etree.fromstring(self._source_object)
        else:
            doc = self.to_xml()
        self.parent_signature = create_relayable_signature(private_key, doc)
        add_element_to_doc(doc, "parent_author_signature", self.parent_signature)
        self.outbound_doc = doc


class DiasporaComment(DiasporaRelayableMixin, Comment):
    """Diaspora comment."""
    def to_xml(self):
        element = etree.Element("comment")
        struct_to_xml(element, [
            {"guid": self.guid},
            {"parent_guid": self.target_guid},
            {"author_signature": self.signature},
            {"parent_author_signature": self.parent_signature},
            {"text": self.raw_content},
            {"diaspora_handle": self.handle},
            {"created_at": format_dt(self.created_at)},
        ])
        return element


class DiasporaPost(DiasporaEntityMixin, Post):
    """Diaspora post, ie status message."""
    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("status_message")
        struct_to_xml(element, [
            {"raw_message": self.raw_content},
            {"guid": self.guid},
            {"diaspora_handle": self.handle},
            {"public": "true" if self.public else "false"},
            {"created_at": format_dt(self.created_at)},
            {"provider_display_name": self.provider_display_name},
        ])
        return element


class DiasporaLike(DiasporaRelayableMixin, Reaction):
    """Diaspora like."""
    reaction = "like"

    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("like")
        struct_to_xml(element, [
            {"target_type": "Post"},
            {"guid": self.guid},
            {"parent_guid": self.target_guid},
            {"author_signature": self.signature},
            {"parent_author_signature": self.parent_signature},
            {"positive": "true"},
            {"diaspora_handle": self.handle},
        ])
        return element


class DiasporaRequest(DiasporaEntityMixin, Relationship):
    """Diaspora legacy request."""
    relationship = "sharing"

    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("request")
        struct_to_xml(element, [
            {"sender_handle": self.handle},
            {"recipient_handle": self.target_handle},
        ])
        return element


class DiasporaContact(DiasporaEntityMixin, Follow):
    """Diaspora contact.

    Note we don't implement 'sharing' at the moment so just send it as the same as 'following'.
    """

    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("contact")
        struct_to_xml(element, [
            {"author": self.handle},
            {"recipient": self.target_handle},
            {"following": "true" if self.following else "false"},
            {"sharing": "true" if self.following else "false"},
        ])
        return element


class DiasporaProfile(DiasporaEntityMixin, Profile):
    """Diaspora profile."""

    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("profile")
        struct_to_xml(element, [
            {"diaspora_handle": self.handle},
            {"first_name": self.name},
            {"last_name": ""},  # Not used in Diaspora modern profiles
            {"image_url": self.image_urls["large"]},
            {"image_url_small": self.image_urls["small"]},
            {"image_url_medium": self.image_urls["medium"]},
            {"gender": self.gender},
            {"bio": self.raw_content},
            {"location": self.location},
            {"searchable": "true" if self.public else "false"},
            {"nsfw": "true" if self.nsfw else "false"},
            {"tag_string": " ".join(["#%s" % tag for tag in self.tag_list])},
        ])
        return element

    @staticmethod
    def fill_extra_attributes(attributes):
        """Diaspora Profile XML message contains no GUID. We need the guid. Fetch it."""
        if not attributes.get("handle"):
            raise ValueError("Can't fill GUID for profile creation since there is no handle! Attrs: %s" % attributes)
        profile = retrieve_and_parse_profile(attributes.get("handle"))
        attributes["guid"] = profile.guid
        return attributes


class DiasporaRetraction(DiasporaEntityMixin, Retraction):
    """Diaspora Retraction."""
    mapped = {
        "Like": "Reaction",
        "Photo": "Image",
        "Person": "Profile",
    }

    def to_xml(self):
        """Convert to XML message."""
        element = etree.Element("retraction")
        struct_to_xml(element, [
            {"author": self.handle},
            {"target_guid": self.target_guid},
            {"target_type": DiasporaRetraction.entity_type_to_remote(self.entity_type)},
        ])
        return element

    @staticmethod
    def entity_type_from_remote(value):
        """Convert entity type between Diaspora names and our Entity names."""
        if value in DiasporaRetraction.mapped:
            return DiasporaRetraction.mapped[value]
        return value

    @staticmethod
    def entity_type_to_remote(value):
        """Convert entity type between our Entity names and Diaspora names."""
        if value in DiasporaRetraction.mapped.values():
            values = list(DiasporaRetraction.mapped.values())
            index = values.index(value)
            return list(DiasporaRetraction.mapped.keys())[index]
        return value
