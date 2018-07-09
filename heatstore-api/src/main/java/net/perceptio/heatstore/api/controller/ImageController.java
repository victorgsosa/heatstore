package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.ImageRepository;
import net.perceptio.heatstore.api.model.Image;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/image-api")
@SuppressWarnings("unused")
public class ImageController {
    static Logger log = LoggerFactory.getLogger(ImageController.class);

    private ImageRepository repository;


    @PostMapping(value = "/image")
    public Image saveImage(@RequestBody Image image) {
        image.setDetections(image.getDetections().stream().map(detection -> {
            detection.setImage(image);
            return detection;
        }).collect(Collectors.toList()));
        return getRepository().save(image);
    }

    @GetMapping(value = "/images")
    public @ResponseBody
    List<Image> findImages(@RequestParam("init") Date init, @RequestParam(value = "end", required = false) Date end) {
        List<Image> images = getRepository().findByDateBetween(init, end);
        log.debug("Images found: {}", images);
        return images;
    }


    public ImageRepository getRepository() {
        return repository;
    }

    @Autowired
    public void setRepository(ImageRepository repository) {
        this.repository = repository;
    }
}
