package net.perceptio.heatstore.api.config;

import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.lookup.JndiDataSourceLookup;

import javax.naming.NamingException;
import javax.sql.DataSource;


@Configuration
@EntityScan({"net.perceptio.heatstore.api.model"})
@EnableJpaRepositories({"net.perceptio.heatstore.api.controller.repository"})
@SuppressWarnings("unused")
public class CloudConfiguration {

    @Bean(destroyMethod = "")
    public DataSource jndiDataSource() throws IllegalArgumentException, NamingException {
        JndiDataSourceLookup dataSourceLookup = new JndiDataSourceLookup();
        dataSourceLookup.setResourceRef(true);
        DataSource ds = dataSourceLookup.getDataSource("java:comp/env/jdbc/DefaultDB");
        return ds;
    }
}
