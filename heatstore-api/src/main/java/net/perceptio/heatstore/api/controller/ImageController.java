package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.DetectionsCountRepository;
import net.perceptio.heatstore.api.controller.repository.ImageRepository;
import net.perceptio.heatstore.api.model.DetectionsCount;
import net.perceptio.heatstore.api.model.Image;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.sql.Timestamp;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/image-api")
@SuppressWarnings("unused")
public class ImageController {
    static Logger log = LoggerFactory.getLogger(ImageController.class);

    private ImageRepository ImageRepository;
    private DetectionsCountRepository detectionsCountRepository;


    @CrossOrigin
    @PostMapping("/image")
    public Image saveImage(@RequestBody Image image) {
        image.setDetections(image.getDetections().stream().map(detection -> {
            detection.setImage(image);
            return detection;
        }).collect(Collectors.toList()));
        return getImageRepository().save(image);
    }

    @CrossOrigin
    @GetMapping("/images")
    public @ResponseBody
    List<Image> findImages(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<Image> images = getImageRepository().findByDateBetween(new Timestamp(init.getTime()), new Timestamp(end.getTime()));
        log.debug("Images found: {}", images);
        return images;
    }

    @CrossOrigin
    @GetMapping("detectionsCount")
    public @ResponseBody
    List<DetectionsCount> findDetectionsCount(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<DetectionsCount> detectionsCounts = getDetectionsCountRepository().findByIdDateBetween(init, end);
        log.debug("Detections count found {}", detectionsCounts);
        return detectionsCounts;
    }

    @CrossOrigin
    @GetMapping("detectionsCount/groupByHour")
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
}
