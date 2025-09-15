# bookshelf app - Permissions and Groups

Custom permissions defined on Book model:
- can_view   -> View books
- can_create -> Create books
- can_edit   -> Edit books
- can_delete -> Delete books

Views are protected using @permission_required decorators:
- list_books -> bookshelf.can_view
- create_book -> bookshelf.can_create
- edit_book -> bookshelf.can_edit
- delete_book -> bookshelf.can_delete

Assign permissions to groups (Editors, Viewers, Admins) via Django admin.
