import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Ensure OAUTHLIB_INSECURE_TRANSPORT and RELAX_TOKEN_SCOPE are set for local development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))


