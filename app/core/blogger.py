import os
import markdown
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']

class BloggerPublisher:
    def __init__(self, client_secrets_file: str = "client_secret.json", token_file: str = "token.json"):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.service = None

    def authenticate(self) -> bool:
        """Handles OAuth 2.0 flow. Generates token.json on first login so users never need to re-login."""
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.client_secrets_file):
                    raise FileNotFoundError(
                        f"Missing '{self.client_secrets_file}'. Download OAuth 2.0 Client credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = build('blogger', 'v3', credentials=creds)
        return True

    def markdown_to_blogger_html(self, md_content: str) -> str:
        """Converts Markdown into responsive, styled HTML suited for modern Blogger themes."""
        raw_html = markdown.markdown(md_content, extensions=['extra', 'tables'])
        
        styled_html = f"""
<div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.7; color: #222;">
{raw_html}
</div>
<style>
  div img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 16px 0; }}
  h1, h2, h3 {{ color: #111; margin-top: 24px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
  th {{ background-color: #f7f7f7; }}
  blockquote {{ border-left: 4px solid #1E88E5; padding-left: 12px; color: #555; margin: 16px 0; }}
</style>
"""
        return styled_html

    def publish_post(self, blog_id: str, title: str, md_content: str, tags: Optional[List[str]] = None, is_draft: bool = False) -> dict:
        """Publishes or drafts a post on Blogger."""
        if not self.service:
            self.authenticate()

        html_content = self.markdown_to_blogger_html(md_content)
        
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": html_content,
            "labels": tags or []
        }

        posts_resource = self.service.posts()
        request = posts_resource.insert(blogId=blog_id, body=body, isDraft=is_draft)
        response = request.execute()
        return response
