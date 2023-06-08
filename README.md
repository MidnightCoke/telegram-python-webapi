# figensoft-telegram-python-webapi
###
__Request model for /bulkmessage/1_n :__
```json
{
    "data": {
        "phone_numbers": ["905414878554", "905076154292"],
        "message": "Test bulk ordinary message"
    },
    "config": {
        "api_id":"your_api_id",
        "api_hash":"your_api_hash",
        "session_id": "your_session_name"
    }
}
```

__Request model for /bulkmessage/n_n :__
```json
{
    "data": [
        {
            "phone_number": "905439619330",
            "message": "test web api 1"
        },
        {
            "phone_number": "905414878554",
            "message": "test web api 2"
        },
        {
            "phone_number": "905076154292",
            "message": "test web api 3"
        }
    ],
    "config": {
        "api_id":"your_api_id",
        "api_hash":"your_api_hash",
        "session_id": "your_session_name"
    }
}
```

