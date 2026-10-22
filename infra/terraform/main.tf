resource "azurerm_resource_group" "payments" {
  name     = "${var.name_prefix}-rg"
  location = var.location
  tags     = var.tags
}

resource "azurerm_container_registry" "payments" {
  name                = replace("${var.name_prefix}acr", "-", "")
  resource_group_name = azurerm_resource_group.payments.name
  location            = azurerm_resource_group.payments.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = var.tags
}

resource "azurerm_kubernetes_cluster" "payments" {
  name                = "${var.name_prefix}-aks"
  location            = azurerm_resource_group.payments.location
  resource_group_name = azurerm_resource_group.payments.name
  dns_prefix          = "${var.name_prefix}-demo"
  sku_tier            = "Free"
  private_cluster_enabled = true
  local_account_disabled  = true
  oidc_issuer_enabled     = true
  workload_identity_enabled = true
  role_based_access_control_enabled = true
  azure_active_directory_role_based_access_control {
    azure_rbac_enabled = true
  }
  default_node_pool {
    name       = "system"
    node_count = 1
    vm_size    = var.node_vm_size
  }
  identity {
    type = "SystemAssigned"
  }
  tags = var.tags
}

resource "azurerm_role_assignment" "cluster_acr_pull" {
  scope                = azurerm_container_registry.payments.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.payments.kubelet_identity[0].object_id
}
