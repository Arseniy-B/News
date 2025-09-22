from fastapi import Request


def login_required(request: Request):
    print('login required') 

