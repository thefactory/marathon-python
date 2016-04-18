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

  Scenario: Events can be listened in stream
    Given a working marathon instance
	 When marathon version is greater than 0.11.0
	  And we start listening for events
      And we create a trivial new app
      And we wait the trivial app deployment finish
     Then we should be able to kill the tasks
	  And we should see list of events
