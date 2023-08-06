from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from aristotle_mdr import perms
from aristotle_mdr.utils import fetch_aristotle_settings


class AristotleBackend(ModelBackend):
    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if the requested app is an aristotle extension.
        Actual permissions to edit/change content are covered in aristotle_mdr.admin
        Otherwise, it returns as per Django permissions
        """
        if not user_obj.is_active:
            return False
        extensions = fetch_aristotle_settings().get('CONTENT_EXTENSIONS', [])
        if app_label in extensions + ["aristotle_mdr"]:
            return perms.user_is_editor(user_obj)
        return super(AristotleBackend, self).has_module_perms(user_obj, app_label)

    def has_perm(self, user_obj, perm, obj=None):

        if not user_obj.is_active:
            return False
        if user_obj.is_superuser:
            return True

        app_label, perm_name = perm.split('.', 1)
        extensions = fetch_aristotle_settings().get('CONTENT_EXTENSIONS', [])

        if app_label == "aristotle_mdr" and hasattr(perms, perm_name):
            return getattr(perms, perm_name)(user_obj, obj)

        if app_label in extensions + ["aristotle_mdr"]:
            # This is required so that a user can correctly delete the 'concept' parent class in the admin site.
            if perm_name == "delete_concept_from_admin":
                return obj is None or perms.user_can_edit(user_obj, obj)

            # This is a rough catch all, and is designed to indicate a user could
            # delete an item type, but not a specific item.
            elif (
                perm_name.startswith('delete_') or
                perm_name.startswith('create_') or
                perm_name.startswith('add_')
            ):
                if obj is None:
                    return perms.user_is_editor(user_obj)
                else:
                    return perms.user_can_edit(user_obj, obj)

        return super(AristotleBackend, self).has_perm(user_obj, perm, obj)
