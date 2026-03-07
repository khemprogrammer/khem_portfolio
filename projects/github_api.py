import requests
from datetime import datetime
from django.conf import settings
from django.utils import timezone


class GitHubAPI:
    """GitHub API integration for fetching repository data"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        self.username = getattr(settings, 'GITHUB_USERNAME', 'khemprogrammer')
        self.token = getattr(settings, 'GITHUB_TOKEN', '')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Django-Portfolio'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def _make_request(self, endpoint):
        """Make authenticated request to GitHub API"""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GitHub API Error: {e}")
            return None
    
    def get_user_profile(self):
        """Fetch GitHub user profile"""
        data = self._make_request(f"/users/{self.username}")
        if data:
            return {
                'username': data.get('login'),
                'name': data.get('name'),
                'avatar_url': data.get('avatar_url'),
                'bio': data.get('bio'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'html_url': data.get('html_url'),
                'blog': data.get('blog'),
                'location': data.get('location'),
                'company': data.get('company'),
                'created_at': data.get('created_at'),
            }
        return None
    
    def get_repositories(self, per_page=100, sort='updated', exclude_forks=True):
        """Fetch user's public repositories"""
        endpoint = f"/users/{self.username}/repos?per_page={per_page}&sort={sort}&direction=desc"
        data = self._make_request(endpoint)
        
        if not data:
            return []
        
        repos = []
        for repo in data:
            # Skip forks if requested
            if exclude_forks and repo.get('fork'):
                continue
            
            repos.append({
                'id': repo.get('id'),
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'description': repo.get('description', ''),
                'html_url': repo.get('html_url'),
                'homepage': repo.get('homepage'),
                'language': repo.get('language'),
                'stargazers_count': repo.get('stargazers_count', 0),
                'forks_count': repo.get('forks_count', 0),
                'open_issues_count': repo.get('open_issues_count', 0),
                'created_at': repo.get('created_at'),
                'updated_at': repo.get('updated_at'),
                'pushed_at': repo.get('pushed_at'),
                'topics': repo.get('topics', []),
                'is_private': repo.get('private', False),
                'is_fork': repo.get('fork', False),
            })
        
        return repos
    
    def get_repository(self, repo_name):
        """Fetch specific repository details"""
        data = self._make_request(f"/repos/{self.username}/{repo_name}")
        
        if not data:
            return None
        
        return {
            'id': data.get('id'),
            'name': data.get('name'),
            'full_name': data.get('full_name'),
            'description': data.get('description', ''),
            'html_url': data.get('html_url'),
            'homepage': data.get('homepage'),
            'language': data.get('language'),
            'stargazers_count': data.get('stargazers_count', 0),
            'forks_count': data.get('forks_count', 0),
            'open_issues_count': data.get('open_issues_count', 0),
            'watchers_count': data.get('watchers_count', 0),
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
            'pushed_at': data.get('pushed_at'),
            'topics': data.get('topics', []),
            'default_branch': data.get('default_branch'),
            'size': data.get('size'),
        }
    
    def get_languages(self, repo_name):
        """Fetch languages used in a repository"""
        data = self._make_request(f"/repos/{self.username}/{repo_name}/languages")
        return data if data else {}
    
    def get_contributions(self):
        """Get contribution statistics (simplified)"""
        repos = self.get_repositories(per_page=100)
        total_commits = 0
        languages = {}
        
        for repo in repos[:10]:  # Limit to avoid rate limiting
            repo_langs = self.get_languages(repo['name'])
            for lang, bytes_count in repo_langs.items():
                languages[lang] = languages.get(lang, 0) + bytes_count
        
        # Sort languages by usage
        sorted_languages = sorted(
            languages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        return {
            'total_repos': len(repos),
            'top_languages': [
                {'name': lang, 'bytes': bytes_count}
                for lang, bytes_count in sorted_languages
            ]
        }
    
    def get_user_stats(self):
        """Get comprehensive user statistics"""
        profile = self.get_user_profile()
        repos = self.get_repositories(per_page=100)
        
        if not profile:
            return self._get_default_stats()
        
        # Calculate total stars and forks
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        
        # Get language statistics
        languages = {}
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        # Sort languages
        top_languages = sorted(
            languages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:6]
        
        return {
            'profile': profile,
            'total_repos': profile.get('public_repos', 0),
            'followers': profile.get('followers', 0),
            'following': profile.get('following', 0),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'top_languages': [
                {'name': lang, 'count': count}
                for lang, count in top_languages
            ],
            'recent_repos': repos[:6],
            'error': False
        }
    
    def _get_default_stats(self):
        """Return default stats when API fails"""
        return {
            'profile': None,
            'total_repos': 0,
            'followers': 0,
            'following': 0,
            'total_stars': 0,
            'total_forks': 0,
            'top_languages': [],
            'recent_repos': [],
            'error': True
        }