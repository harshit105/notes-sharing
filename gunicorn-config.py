#host and port where our app will run
bind = '127.0.0.1:5000'

# Average Requests per Second (Round robin)= (Number of Workers × Concurrency per Worker)/Rate Limit
workers = 5
