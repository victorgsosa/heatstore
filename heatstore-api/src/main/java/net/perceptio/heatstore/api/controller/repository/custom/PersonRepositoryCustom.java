package net.perceptio.heatstore.api.controller.repository.custom;

import net.perceptio.heatstore.api.model.Embeddings;
import net.perceptio.heatstore.api.model.Person;

import java.util.Collection;

public interface PersonRepositoryCustom {
    Collection<Person> findNear(Collection<Embeddings> embeddings, Double distanceThreshold);
}
