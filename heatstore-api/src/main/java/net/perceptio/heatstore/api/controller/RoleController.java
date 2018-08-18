package net.perceptio.heatstore.api.controller;

import net.perceptio.heatstore.api.controller.repository.RoleRepository;
import net.perceptio.heatstore.api.model.Role;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController("roles")
public class RoleController {

    private RoleRepository repository;

    @CrossOrigin
    @GetMapping("/{id}")
    public Role findOne(@PathVariable("id") String id) {
        return getRepository().findOne(id);
    }

    public RoleRepository getRepository() {
        return repository;
    }

    @Autowired
    public void setRepository(RoleRepository repository) {
        this.repository = repository;
    }
}
