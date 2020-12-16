
class Config:
    # route name
    API_ROUTE = '/api'
    ROUTE = {
        'API': {
            'USER': API_ROUTE + '/user/<int:user_id>',
            'USERS': API_ROUTE + '/user',
            'LOGIN': API_ROUTE + '/login',
            'BOOKS': API_ROUTE + '/book',
            'BOOK': API_ROUTE + '/book/<int:book_id>'
        }
    }