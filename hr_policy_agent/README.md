# HR Policy Agent

HR Policy Agent folder with all necessary files for deployment to Railway.

## Files Included

- **a2a_wrapper_hr_policy_agent.py**: A2A wrapper for the HR Policy Agent with server initialization
- **hr_policy_agent.py**: HR Policy Agent implementation using LangChain and MCP
- **hr_policy_server.py**: FastMCP server for handling HR policy queries using vector store
- **hr_policy_document.pdf**: HR policy document (placeholder)
- **Dockerfile**: Docker configuration for containerization
- **requirements.txt**: Python dependencies
- **railway.json**: Railway deployment configuration
- **README.md**: This file

## Setup Instructions

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   CO_API_KEY=your_cohere_api_key
   ```

3. Run the server:
   ```bash
   python a2a_wrapper_hr_policy_agent.py
   ```

## Deployment to Railway

1. Push the folder to your Git repository on the `hr_policy_agent` branch
2. Connect your repository to Railway
3. Deploy using the `railway.json` configuration

## Notes

- Replace `hr_policy_document.pdf` with your actual HR policy document
- Update the MCP server configuration as needed
- Ensure all environment variables are properly set in Railway