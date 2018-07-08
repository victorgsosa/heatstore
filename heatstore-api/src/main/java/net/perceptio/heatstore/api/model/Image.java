package net.perceptio.heatstore.api.model;

import lombok.Builder;
import lombok.Data;

import java.sql.Date;
import java.util.List;
import java.util.UUID;

@Data
@Builder
public class Image {
    private UUID id;
    private Date date;
    private List<Detection> detections;
}
