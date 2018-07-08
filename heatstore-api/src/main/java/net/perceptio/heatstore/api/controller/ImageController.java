package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.ImageRepository;
import net.perceptio.heatstore.api.model.Image;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/image-api")
@SuppressWarnings("unused")
public class ImageController {

    private ImageRepository repository;


    @RequestMapping(method = RequestMethod.POST, value = "image")
    public Image saveImage(Image image) {
        return getRepository().save(image);
    }


    public ImageRepository getRepository() {
        return repository;
    }

    @Autowired
    public void setRepository(ImageRepository repository) {
        this.repository = repository;
    }
}
