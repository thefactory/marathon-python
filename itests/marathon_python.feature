Feature: marathon-python can create and list marathon apps

  Scenario: Trivial apps can be deployed
    Given a working marathon instance
    When we create a trivial new app
    Then we should see it running via the marathon api
