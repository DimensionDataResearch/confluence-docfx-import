package io.tintoy.confluence.plugin.docfx_import.impl;

import com.atlassian.plugin.spring.scanner.annotation.export.ExportAsService;
import com.atlassian.plugin.spring.scanner.annotation.imports.ComponentImport;
import com.atlassian.sal.api.ApplicationProperties;
import io.tintoy.confluence.plugin.docfx_import.api.PluginComponent;

import javax.inject.Inject;
import javax.inject.Named;

@ExportAsService ({PluginComponent.class})
@Named ("pluginComponent")
public class PluginComponentImpl implements PluginComponent
{
    @ComponentImport
    private final ApplicationProperties applicationProperties;

    @Inject
    public PluginComponentImpl(final ApplicationProperties applicationProperties)
    {
        this.applicationProperties = applicationProperties;
    }

    public String getName()
    {
        if(applicationProperties != null)
            return "pluginComponent:" + applicationProperties.getDisplayName();
        
        return "pluginComponent";
    }
}