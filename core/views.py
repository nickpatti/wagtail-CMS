import json

from django.http import JsonResponse

from core.request_handler import send_feedback


def submit_feedback(request):
    post_body = request.POST

    # Always returns is_useful True as this field is required by the API but no longer in the form
    feedback_obj = {'is_useful': True, 'questions': []}
    for key, value in post_body.items():
        if key == 'page':
            feedback_obj[key] = value
        elif key == 'user_feedback':
            feedback_obj.get('questions').append({
                'title': 'howwasthisuseful',
                'feedback': value
            })
            # Always returns title howwasthisuseful as this field is expected by the API and the  current one isn't

    response = send_feedback(json.dumps(feedback_obj))

    if response.ok:
        response_body = {}
    else:
        response_body = response.json()
    return JsonResponse(response_body, status=response.status_code)
