package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.CameraRepository;
import net.perceptio.heatstore.api.model.Camera;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/cameras")
@SuppressWarnings("unused")
public class CameraController {

    private CameraRepository repository;

    @CrossOrigin
    @GetMapping("/{id}")
    public Optional<Camera> findOne(@PathVariable("id") String id) {
        return getRepository().findById(id);
    }

    public CameraRepository getRepository() {
        return repository;
    }

    @Autowired
    public void setRepository(CameraRepository repository) {
        this.repository = repository;
    }
}
