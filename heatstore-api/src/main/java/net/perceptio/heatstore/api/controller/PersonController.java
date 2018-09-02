package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.ImageRepository;
import net.perceptio.heatstore.api.controller.repository.PersonRepository;
import net.perceptio.heatstore.api.model.Embeddings;
import net.perceptio.heatstore.api.model.Image;
import net.perceptio.heatstore.api.model.Person;
import net.perceptio.heatstore.api.properties.PersonProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Timestamp;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/persons")
@SuppressWarnings("unused")
public class PersonController {
    private static final Logger logger = LoggerFactory.getLogger(PersonController.class);
    public PersonProperties properties;
    private PersonRepository repository;
    private ImageRepository imageRepository;

    @PutMapping
    private Person save(@RequestBody Person person) {
        logger.debug("Saving person {}", person);
        Timestamp seenOn = new Timestamp(System.currentTimeMillis());
        if (person.getId() == null) {
            logger.debug("Trying to find near person to {}", person);
            List<Person> persons = new ArrayList(findNear(person.getEmbeddings()));
            if (!persons.isEmpty()) {
                Person oldPerson = persons.get(0);
                logger.debug("Near person found, updating: {}", oldPerson);
                oldPerson.setLastSeenOn(seenOn);
                if (person.getImages().stream().anyMatch(i -> oldPerson.getImages().contains(i))) {
                    throw new IllegalArgumentException(
                            String.format("This person had been already detected this images %s", person.getImages()));
                }
                oldPerson.addImages(person.getImages());
                person = oldPerson;
            } else {
                logger.debug("Person does not have a near person, inserting {}", person);
                person.setFirstSeenOn(seenOn);
                person.setLastSeenOn(seenOn);
            }
        } else {
            person.setFirstSeenOn(seenOn);
            person.setLastSeenOn(seenOn);
        }
        checkPerson(person);
        person = getRepository().save(person);
        logger.debug("Person saved: {}", person);
        return person;
    }

    private Person checkPerson(Person person) {
        Set<Image> images = new HashSet<>();
        for (Image image : person.getImages()) {
            if (image.getId() == null) {
                images.add(image);
            } else {
                images.add(getImageRepository().findById(image.getId())
                        .orElseThrow(() -> new IllegalArgumentException(
                                String.format("Image %d does not exists ", image.getId())))
                );
            }
        }
        person.setImages(images);
        return person;
    }

    @GetMapping("/near")
    public Collection<Person> findNear(@RequestParam Map<String, String> e) {
        logger.debug("Finding persons with distance {} near to {}", getProperties().getThreshold(), e);
        List<Embeddings> embeddings = e.entrySet().stream()
                .map(entry -> new Embeddings(null, Integer.parseInt(entry.getKey()), Double.parseDouble(entry.getValue())))
                .collect(Collectors.toList());
        return findNear(embeddings);
    }

    public Collection<Person> findNear(Collection<Embeddings> embeddings) {
        Collection<Person> nearPersons = getRepository().findNear(embeddings, getProperties().getThreshold());
        return nearPersons.stream().map(p -> getRepository().findById(p.getId()).get()).collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public Optional<Person> findById(@PathVariable("id") Long id) {
        return getRepository().findById(id);
    }


    public PersonRepository getRepository() {
        return repository;
    }

    @Autowired
    public void setRepository(PersonRepository repository) {
        this.repository = repository;
    }

    public ImageRepository getImageRepository() {
        return imageRepository;
    }

    @Autowired
    public void setImageRepository(ImageRepository imageRepository) {
        this.imageRepository = imageRepository;
    }

    public PersonProperties getProperties() {
        return properties;
    }

    @Autowired
    public void setProperties(PersonProperties properties) {
        this.properties = properties;
    }
}
