package net.perceptio.heatstore.api.controller.repository;


import net.perceptio.heatstore.api.model.Image;
import org.springframework.data.repository.Repository;

import java.sql.Date;
import java.util.List;
import java.util.UUID;


public interface ImageRepository extends Repository<Image, UUID> {
    @SuppressWarnings("unused")
    Image save(Image image);

    @SuppressWarnings("unused")
    Image findById(UUID id);

    List<Image> findByDateBetween(Date init, Date end);


}
