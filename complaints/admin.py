from django.contrib import admin
from django.utils import timezone
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'user', 'created_at')
    list_editable = ('status',)
    list_filter = ('category', 'status', 'user')
    search_fields = ('title', 'description', 'location', 'user__username')
    readonly_fields = ('created_at',)
    actions = ('mark_in_progress', 'mark_resolved', 'mark_rejected')

    def _append_remark(self, complaint, request, note):
        ts = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        prefix = f"[Admin:{request.user.username} {ts}] "
        if complaint.remarks:
            complaint.remarks = f"{complaint.remarks}\n{prefix}{note}"
        else:
            complaint.remarks = f"{prefix}{note}"

    def mark_in_progress(self, request, queryset):
        updated = 0
        for c in queryset:
            c.status = 'In Progress'
            self._append_remark(c, request, 'Marked In Progress')
            c.save()
            updated += 1
        self.message_user(request, f"{updated} complaint(s) marked In Progress.")
    mark_in_progress.short_description = 'Mark selected complaints as In Progress'

    def mark_resolved(self, request, queryset):
        updated = 0
        for c in queryset:
            c.status = 'Resolved'
            self._append_remark(c, request, 'Marked Resolved')
            c.save()
            updated += 1
        self.message_user(request, f"{updated} complaint(s) marked Resolved.")
    mark_resolved.short_description = 'Mark selected complaints as Resolved'

    def mark_rejected(self, request, queryset):
        updated = 0
        for c in queryset:
            c.status = 'Rejected'
            self._append_remark(c, request, 'Marked Rejected')
            c.save()
            updated += 1
        self.message_user(request, f"{updated} complaint(s) marked Rejected.")
    mark_rejected.short_description = 'Mark selected complaints as Rejected'
