$token = Read-Host -Prompt "Enter your token" -AsSecureString | ConvertFrom-SecureString
uv build
uv publish --token $token