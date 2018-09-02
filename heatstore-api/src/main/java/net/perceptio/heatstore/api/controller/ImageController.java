package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.CameraRepository;
import net.perceptio.heatstore.api.controller.repository.DetectionsCountRepository;
import net.perceptio.heatstore.api.controller.repository.ImageRepository;
import net.perceptio.heatstore.api.model.Camera;
import net.perceptio.heatstore.api.model.DetectionsCount;
import net.perceptio.heatstore.api.model.Image;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.sql.Timestamp;
import java.util.List;

@RestController
@RequestMapping("/images")
@SuppressWarnings("unused")
public class ImageController {
    static Logger log = LoggerFactory.getLogger(ImageController.class);

    private ImageRepository ImageRepository;
    private DetectionsCountRepository detectionsCountRepository;
    private CameraRepository cameraRepository;


    @CrossOrigin
    @PostMapping
    public Image saveImage(@RequestBody Image image) {
        image = checkImage(image);
        return getImageRepository().save(image);
    }

    private Image checkImage(Image image) {
        Camera camera = getCameraRepository().findById(image.getCamera().getId())
                .orElseThrow(() ->
                        new IllegalArgumentException(String.format("Camera %s does not exists", image.getCamera().getId())
                        ));
        image.setCamera(camera);
        return image;
    }

    @CrossOrigin
    @GetMapping
    public @ResponseBody
    List<Image> findImages(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<Image> images = getImageRepository().findByDateBetween(new Timestamp(init.getTime()), new Timestamp(end.getTime()));
        log.debug("Images found: {}", images);
        return images;
    }

    @CrossOrigin
    @GetMapping("/detectionsCount")
    public @ResponseBody
    List<DetectionsCount> findDetectionsCount(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<DetectionsCount> detectionsCounts = getDetectionsCountRepository().findByIdDateBetween(init, end);
        log.debug("Detections count found {}", detectionsCounts);
        return detectionsCounts;
    }

    @CrossOrigin
    @GetMapping("/detectionsCount/groupByHour")
    public @ResponseBody
    List<DetectionsCount> findDetectionsCountGroupByHour(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<DetectionsCount> detectionsCounts = getDetectionsCountRepository().findByIdDateBetweenGroupByHour(init, end);
        log.debug("Detections count found {}", detectionsCounts);
        return detectionsCounts;
    }


    public ImageRepository getImageRepository() {
        return ImageRepository;
    }

    @Autowired
    public void setImageRepository(ImageRepository imageRepository) {
        this.ImageRepository = imageRepository;
    }


    public DetectionsCountRepository getDetectionsCountRepository() {
        return detectionsCountRepository;
    }

    @Autowired
    public void setDetectionsCountRepository(DetectionsCountRepository detectionsCountRepository) {
        this.detectionsCountRepository = detectionsCountRepository;
    }

    public CameraRepository getCameraRepository() {
        return cameraRepository;
    }

    @Autowired
    public void setCameraRepository(CameraRepository cameraRepository) {
        this.cameraRepository = cameraRepository;
    }
}
