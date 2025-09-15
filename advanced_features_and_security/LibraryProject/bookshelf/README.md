# Permissions & Groups in advanced_features_and_security

- CustomUser model extends `AbstractUser` with fields:
  - `date_of_birth`
  - `profile_photo`
- CustomUserManager implements:
  - `create_user`
  - `create_superuser`
- `AUTH_USER_MODEL` is set in `settings.py`
- Book model has custom permissions:
  - `can_create`
  - `can_edit`
  - `can_delete`
  - `can_view`
- Permissions are enforced in views with `@permission_required`.
- Groups can be created in the Django Admin (`Viewers`, `Editors`, `Admins`) and assigned permissions accordingly.
