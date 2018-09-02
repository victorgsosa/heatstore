package net.perceptio.heatstore.api.controller.repository;

import net.perceptio.heatstore.api.model.Camera;
import org.springframework.data.repository.Repository;

import java.util.Optional;

public interface CameraRepository extends Repository<Camera, String> {
    Optional<Camera> findById(String id);
}
