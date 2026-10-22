output "resource_group_name" {
  value = azurerm_resource_group.payments.name
}

output "acr_login_server" {
  value = azurerm_container_registry.payments.login_server
}
}
