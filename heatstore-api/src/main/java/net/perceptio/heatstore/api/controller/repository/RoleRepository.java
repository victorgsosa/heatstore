package net.perceptio.heatstore.api.controller.repository;

import net.perceptio.heatstore.api.model.Role;
import org.springframework.data.repository.Repository;

public interface RoleRepository extends Repository<Role, String> {
    Role findOne(String id);
}
