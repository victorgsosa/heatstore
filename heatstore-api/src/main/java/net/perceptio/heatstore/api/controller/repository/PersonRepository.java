package net.perceptio.heatstore.api.controller.repository;

import net.perceptio.heatstore.api.controller.repository.custom.PersonRepositoryCustom;
import net.perceptio.heatstore.api.model.Person;
import org.springframework.data.repository.Repository;

import java.util.Collection;
import java.util.Optional;

public interface PersonRepository extends Repository<Person, Long>, PersonRepositoryCustom {

    Person save(Person person);

    Collection<Person> saveAll(Iterable<Person> persons);

    Optional<Person> findById(Long id);

}
