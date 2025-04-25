Backend RESTdjango
Auth from user/urls
POST /api/auth/token ->  access, refresh //Login
POST /api/auth/token/refresh -> new access //renew access
GET /api/auth/whoami/ //return id, username, email, role: [student, teacher, admin]

SIMPLE_JWT
token_life : 15 min
refresh_token : 7 day
-----------------------------------
Frontend (Vue3 + axios + vuex)
