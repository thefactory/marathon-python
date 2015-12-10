Feature: marathon-python can create and list marathon apps

  Scenario: Metadata can be fetched
    Given a working marathon instance
     Then we get the marathon instance's info

  Scenario: Trivial apps can be deployed
    Given a working marathon instance
     When we create a trivial new app
     Then we should see the trivial app running via the marathon api

 Scenario: Complex apps can be deployed
    Given a working marathon instance
     When we create a complex new app
     Then we should see the complex app running via the marathon api
