from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice, LeaveRequest
from .forms import NoticeForm, LeaveRequestForm
from apps.core.decorators import role_required, ADMIN_ROLES, TEACHER_ROLES, ALL_ROLES


@login_required
@role_required(*ALL_ROLES)
def notice_list(request):
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'notices/notice_list.html', {'notices': notices})


@login_required
@role_required(*TEACHER_ROLES)
def notice_add(request):
    form = NoticeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        notice = form.save(commit=False)
        notice.created_by = request.user
        notice.save()
        messages.success(request, 'Notice published!')
        return redirect('notice_list')
    return render(request, 'notices/notice_form.html', {'form': form})


@login_required
@role_required(*ALL_ROLES)
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notices/notice_detail.html', {'notice': notice})


@login_required
@role_required(*ALL_ROLES)
def leave_list(request):
    if request.user.role in ['super_admin', 'principal']:
        leaves = LeaveRequest.objects.select_related('applicant').order_by('-created_at')
    else:
        leaves = LeaveRequest.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, 'notices/leave_list.html', {'leaves': leaves})


@login_required
@role_required(*ALL_ROLES)
def leave_apply(request):
    form = LeaveRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        leave = form.save(commit=False)
        leave.applicant = request.user
        leave.save()
        messages.success(request, 'Leave application submitted!')
        return redirect('leave_list')
    return render(request, 'notices/leave_form.html', {'form': form})


@login_required
@role_required(*ADMIN_ROLES)
def leave_review(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        leave.status = 'approved' if action == 'approve' else 'rejected'
        leave.reviewed_by = request.user
        leave.review_remarks = request.POST.get('remarks', '')
        leave.save()
        messages.success(request, f'Leave {leave.status}.')
        return redirect('leave_list')
    return render(request, 'notices/leave_review.html', {'leave': leave})
