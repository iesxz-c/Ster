from app import create_app, skt

# Initialize the app by calling create_app
app = create_app()

if __name__ == '__main__':
    # Run the SocketIO server
    skt.run(app, host='0.0.0.0', port=5000, debug=True)
