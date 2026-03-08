import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Ensure OAUTHLIB_INSECURE_TRANSPORT is set for local development
    if os.environ.get('FLASK_DEBUG') == '1' or os.environ.get('FLASK_ENV') == 'development':
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
