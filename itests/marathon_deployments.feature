Feature: marathon-python read deployments

  Scenario: deployments can be read
    Given a working marathon instance
     When we create a trivial new app
     Then we should be able to see a deployment
