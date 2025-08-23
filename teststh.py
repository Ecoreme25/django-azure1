# from django.http import JsonResponse
# from .utilss import is_website_live  # assuming you put the function in utils.py

# def check_website_status(request):
#     url = request.GET.get("url", "https://timopassociates.com.ng/")
#     is_live = is_website_live(url)
#     return JsonResponse({"url": url, "live": is_live})


# Import the requests library
import requests

# Define the function to check if a website is live
def is_website_live(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Example usage
url = "https://timopassociates.com.ng/"
if is_website_live(url):
    print(f"{url} is live ✅")
else:
    print(f"{url} is not reachable ❌")