Feature: marathon-python can operate marathon app tasks

  Scenario: App tasks can be listed
    Given a working marathon instance
     When we create a trivial new app
      And we wait the trivial app deployment finish
     Then we should be able to list tasks of the trivial app

  Scenario: App tasks can be killed
    Given a working marathon instance
     When we create a trivial new app
      And we wait the trivial app deployment finish
     Then we should be able to kill the tasks

  Scenario: A list of app tasks can be killed
    Given a working marathon instance
     When we create a trivial new app
      And we wait the trivial app deployment finish
     Then we should be able to kill the #0,1,2 tasks of the trivial app
