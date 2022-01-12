agent_params = [
    (
        {
        'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Expected-values' : {'platform' : 'Mobile',
                            'browser' : 'No',
                            'device' : 'Android'
                            }
        }
    ),
    (
        {
        'User Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        'Expected values' : {'platform' : 'Mobile',
                            'browser' : 'Chrome',
                            'device' : 'iOS'
                            }
        }
     ),
]

user_agent_dist = dict(agent_params[0])
print(user_agent_dist)
print(user_agent_dist['User-Agent'])
print(user_agent_dist['Expected-values'])
print(user_agent_dist['Expected-values']['platform'])
