a = {"atsConfig": {"jobId": 21, "eventId": 21}}
b = {"sanitiseTestConfig": {"featureConfig": {"redisKeyExpiryInSeconds": 900},
                            "submitPasswordDisabled": {"isEnabled": true, "durationInSeconds": 5000},
                            "vendorInitiateAutomation": {"isEnabled": true},
                            "submitPasswordNeverExpired": {"isEnabled": true, "durationInSeconds": 5000},
                            "nonVendorInitiateAutomation": {"isEnabled": true,
                                                            "performInitiateAutomationAfterSeconds": 900,
                                                            "secondsElapsedFromLastActivityByTestUser": 259200},
                            "scoreFetchInitiateAutomation": {"isEnabled": true,
                                                             "attendingTuElapsedDurationInSeconds": 2000},
                            "scoreFetchReInitiateAutomation": {"isEnabled": true},
                            "passwordExpiredToPasswordDisabled": {"isEnabled": true, "durationInSeconds": 5000}}}

c = {
    "featureConfig":
        {
            "testUserRedisKeyExpiryInSeconds": 120,
            "tenantRedisKeyExpiryInSeconds": 180,
            "testFilters": {
                "testActiveThreshHoldInDays": 10
            },
            "testUserFilters": {
                "loginThreshHoldInDays": 30

            }
        },
    "vendorInitiateAutomation":
        {
            "isEnabled": true
        },
    "scoreFetchReInitiateAutomation":
        {
            "isEnabled": true
        },
    "scoreFetchInitiateAutomation":
        {
            "isEnabled": true,
            "attendingTuElapsedDurationInSeconds": 180
        },
    "passwordExpiredToPasswordDisabled":
        {
            "isEnabled": true,
            "durationInSeconds": 60
        },
    "submitPasswordNeverExpired":
        {
            "isEnabled": true,
            "durationInSeconds": 180
        },
    "submitPasswordDisabled":
        {
            "isEnabled": true,
            "durationInSeconds": 60
        },
    "nonVendorInitiateAutomation":
        {
            "isEnabled": true,
            "performInitiateAutomationAfterSeconds": 60,
            "secondsElapsedFromLastActivityByTestUser": 600
        }
}
