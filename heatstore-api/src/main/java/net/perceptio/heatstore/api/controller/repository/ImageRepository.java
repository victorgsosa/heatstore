package net.perceptio.heatstore.api.controller.repository;


import net.perceptio.heatstore.api.model.Image;
import org.springframework.data.repository.Repository;

import java.sql.Timestamp;
import java.util.List;


public interface ImageRepository extends Repository<Image, Long> {
    @SuppressWarnings("unused")
    Image save(Image image);

    @SuppressWarnings("unused")
    Image findById(Long id);

    List<Image> findByDateBetween(Timestamp init, Timestamp end);


}
