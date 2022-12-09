# Motion-Control-System

Over the past few decades, computing systems have undergone substantial change. 
Additionally, there has been an improvement in how people connect with machines. 
Simple keyboard inputs to sophisticated vision-based gesture recognition systems 
are all examples of Human-Computer Interactions (HCI) techniques.

This project is a mouse simulation system that mimics your hand movements and gestures 
to carry out all the actions your mouse would normally carry out. Simply put, a camera records your video,
and you may move the cursor, make a left click, right click, drag, select, and up and down scroll depending on your hand motions.

# Objective

The objective of the resulting application is to serve as an alternative for mouses and remotes for navigating or interacting with the UI of a computer. The application can be run on any system with python installed, given that it has a webcam and meets the minimum requirements that will be stated in one of the upcoming sections. The application is also meant to increase the ease for physically disabled people.



# Module 1- Palm Detection Model

We developed a single-shot detector model for mobile real-time usage to find first hand locations in a manner comparable to the face recognition model in MediaPipe Face Mesh. Recognize hands that are self- or otherwise occluded in relation to the visual frame. Unlike faces, which have high contrast patterns around the mouth and eyes, it can be difficult to correctly recognise hands from their visual characteristics alone. Instead, adding extra context—such as details of the arm, torso, or person—allows for accurate hand localization.


# Module 2- Hand Landmark Model

Our second hand landmark model employs regression, or direct coordinate prediction, to precisely localize key points for 21 3-D hand-knuckle coordinates inside the observed hand areas after recognising the palm over the whole picture. Self-occlusions and partially visible hands have no effect on the model's ability to establish a trustworthy internal hand position representation.
