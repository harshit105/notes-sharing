#host and port where our app will run
bind = 'web:5000'

# Average Requests per Second (Round robin)= (Number of Workers × Concurrency per Worker)/Rate Limit
workers = 5
