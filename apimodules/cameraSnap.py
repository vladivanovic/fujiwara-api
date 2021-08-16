import meraki


# Defining your API key as a variable in source code is not recommended
API_KEY = '837665f9a0c365cba79382f6bc035676368e602d'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)

serial = 'Q2FV-WZDD-NLJC'

response = dashboard.camera.generateDeviceCameraSnapshot(serial)

print(response)


