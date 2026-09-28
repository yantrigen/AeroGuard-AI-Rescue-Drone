# 'cap.read()' ke turant baad yeh line add karein:
frame = cv2.resize(frame, (640, 480)) # VGA size, standard for YOLO
frame_counter = 0

while True:
    ret, frame = cap.read()
    frame_counter += 1
    
    # Sirf har 3rd frame ko YOLO model me bhejenge
    if frame_counter % 3 == 0:
        results = model.predict(source=frame, conf=0.5, classes=[0], verbose=False)
        annotated_frame = results[0].plot()
    else:
        # Baki frames bina AI ke directly screen par dikhayenge
        annotated_frame = frame
