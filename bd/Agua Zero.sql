-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema aguazero
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema aguazero
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `aguazero` DEFAULT CHARACTER SET utf8 ;
USE `aguazero` ;

-- -----------------------------------------------------
-- Table `aguazero`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Usuarios` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `correo` VARCHAR(45) NULL,
  `password_hash` VARCHAR(256) NULL,
  `tipo` VARCHAR(20) NULL,
  `estatus` CHAR(1) NULL,
  PRIMARY KEY (`idUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`puestos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`puestos` (
  `idPuesto` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `salario_max` VARCHAR(45) NULL,
  `salario_min` VARCHAR(45) NULL,
  `descripcion` VARCHAR(200) NULL,
  PRIMARY KEY (`idPuesto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Empleado` (
  `idEmpleado` INT NOT NULL AUTO_INCREMENT,
  `tipoEmpleado` VARCHAR(40) NULL,
  `salario_por_dia` VARCHAR(45) NULL,
  `turno` VARCHAR(45) NULL,
  `nss` VARCHAR(45) NULL,
  `Usuarios_idUsuario` INT NOT NULL,
  `puestos_idPuesto` INT NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  INDEX `fk_Empleado_Usuarios1_idx` (`Usuarios_idUsuario` ASC) VISIBLE,
  INDEX `fk_Empleado_puestos1_idx` (`puestos_idPuesto` ASC) VISIBLE,
  CONSTRAINT `fk_Empleado_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuario`)
    REFERENCES `aguazero`.`Usuarios` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Empleado_puestos1`
    FOREIGN KEY (`puestos_idPuesto`)
    REFERENCES `aguazero`.`puestos` (`idPuesto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `domicilio` VARCHAR(45) NULL,
  `localidad` VARCHAR(45) NULL,
  `rfc` VARCHAR(15) NULL,
  `Usuarios_idUsuario` INT NOT NULL,
  PRIMARY KEY (`idCliente`),
  INDEX `fk_Cliente_Usuarios1_idx` (`Usuarios_idUsuario` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuario`)
    REFERENCES `aguazero`.`Usuarios` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Vehiculo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Vehiculo` (
  `idVehiculo` INT NOT NULL AUTO_INCREMENT,
  `placas` VARCHAR(10) NULL,
  `tipo_de_vehiculo` VARCHAR(45) NULL,
  `tipo_combustible` VARCHAR(45) NULL,
  `capacidad_tanque` VARCHAR(15) NULL,
  `modelo` VARCHAR(45) NULL,
  `año` CHAR(4) NULL,
  `capacidad_garrafones` INT NULL,
  PRIMARY KEY (`idVehiculo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Repartidor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Repartidor` (
  `idRepartidor` INT NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT NOT NULL,
  `Vehiculo_idVehiculo` INT NOT NULL,
  `ruta` VARCHAR(45) NULL,
  `folio_de_licencia` INT NULL,
  PRIMARY KEY (`idRepartidor`),
  INDEX `fk_Repartidor_Vehiculo1_idx` (`Vehiculo_idVehiculo` ASC) VISIBLE,
  INDEX `fk_Repartidor_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  CONSTRAINT `fk_Repartidor_Vehiculo1`
    FOREIGN KEY (`Vehiculo_idVehiculo`)
    REFERENCES `aguazero`.`Vehiculo` (`idVehiculo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Repartidor_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`Empleado` (`idEmpleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`promociones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`promociones` (
  `idpromocion` INT NOT NULL AUTO_INCREMENT,
  `cantidad_max` INT NULL,
  `cantidad_min` INT NULL,
  `estatus` TINYINT NULL,
  `porcentaje` DOUBLE NULL,
  PRIMARY KEY (`idpromocion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Ventas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Ventas` (
  `idVenta` INT NOT NULL AUTO_INCREMENT,
  `precio_total` DOUBLE NULL,
  `fecha` DATE NULL,
  `estatus` VARCHAR(45) NULL,
  `promociones_idpromocion` INT NOT NULL,
  `Repartidor_idRepartidor` INT NOT NULL,
  PRIMARY KEY (`idVenta`),
  INDEX `fk_Ventas_promociones1_idx` (`promociones_idpromocion` ASC) VISIBLE,
  INDEX `fk_Ventas_Repartidor1_idx` (`Repartidor_idRepartidor` ASC) VISIBLE,
  CONSTRAINT `fk_Ventas_promociones1`
    FOREIGN KEY (`promociones_idpromocion`)
    REFERENCES `aguazero`.`promociones` (`idpromocion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ventas_Repartidor1`
    FOREIGN KEY (`Repartidor_idRepartidor`)
    REFERENCES `aguazero`.`Repartidor` (`idRepartidor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Garrafones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Garrafones` (
  `idGarrafon` INT NOT NULL AUTO_INCREMENT,
  `Estado` VARCHAR(15) NULL,
  `codigo` CHAR(10) NULL,
  `capaciodad` INT NULL,
  `precio_retornable` FLOAT NULL,
  `precio_completo` FLOAT NULL,
  PRIMARY KEY (`idGarrafon`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Prestamos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Prestamos` (
  `idPrestamos` INT NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT NOT NULL,
  `Ventas_idVentas` INT NOT NULL,
  `Garrafones_idGarrafon` INT NOT NULL,
  `Cliente_idCliente` INT NOT NULL,
  PRIMARY KEY (`idPrestamos`),
  INDEX `fk_Prestamos_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  INDEX `fk_Prestamos_Ventas1_idx` (`Ventas_idVentas` ASC) VISIBLE,
  INDEX `fk_Prestamos_Garrafones1_idx` (`Garrafones_idGarrafon` ASC) VISIBLE,
  INDEX `fk_Prestamos_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Prestamos_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`Empleado` (`idEmpleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Prestamos_Ventas1`
    FOREIGN KEY (`Ventas_idVentas`)
    REFERENCES `aguazero`.`Ventas` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Prestamos_Garrafones1`
    FOREIGN KEY (`Garrafones_idGarrafon`)
    REFERENCES `aguazero`.`Garrafones` (`idGarrafon`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Prestamos_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `aguazero`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`nominas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`nominas` (
  `idnomina` INT NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT NOT NULL,
  `salario_total` DOUBLE NULL,
  `dias_trabajados` INT NULL,
  `comisiones` DOUBLE NULL,
  PRIMARY KEY (`idnomina`),
  INDEX `fk_nominas_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  CONSTRAINT `fk_nominas_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`Empleado` (`idEmpleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`factura` (
  `idfactura` INT NOT NULL AUTO_INCREMENT,
  `fecha` VARCHAR(45) NULL,
  `Cliente_idCliente` INT NOT NULL,
  `Ventas_idVenta` INT NOT NULL,
  PRIMARY KEY (`idfactura`),
  INDEX `fk_factura_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  INDEX `fk_factura_Ventas1_idx` (`Ventas_idVenta` ASC) VISIBLE,
  CONSTRAINT `fk_factura_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `aguazero`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_factura_Ventas1`
    FOREIGN KEY (`Ventas_idVenta`)
    REFERENCES `aguazero`.`Ventas` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`tarjetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`tarjetas` (
  `idtarjeta` INT NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT NOT NULL,
  `numero_tarjeta` VARCHAR(45) NULL,
  `banco` VARCHAR(45) NULL,
  PRIMARY KEY (`idtarjeta`),
  INDEX `fk_tarjetas_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  CONSTRAINT `fk_tarjetas_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`Empleado` (`idEmpleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`Pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`Pagos` (
  `idPago` INT NOT NULL AUTO_INCREMENT,
  `nominas_idnomina` INT NOT NULL,
  `fecha` VARCHAR(45) NULL,
  `realizo` TINYINT NULL,
  `tarjetas_idtarjeta` INT NOT NULL,
  PRIMARY KEY (`idPago`),
  INDEX `fk_Pagos_nominas1_idx` (`nominas_idnomina` ASC) VISIBLE,
  INDEX `fk_Pagos_tarjetas1_idx` (`tarjetas_idtarjeta` ASC) VISIBLE,
  CONSTRAINT `fk_Pagos_nominas1`
    FOREIGN KEY (`nominas_idnomina`)
    REFERENCES `aguazero`.`nominas` (`idnomina`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pagos_tarjetas1`
    FOREIGN KEY (`tarjetas_idtarjeta`)
    REFERENCES `aguazero`.`tarjetas` (`idtarjeta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`ventas_detalle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`ventas_detalle` (
  `idventas_detalle` INT NOT NULL AUTO_INCREMENT,
  `Garrafones_idGarrafon` INT NOT NULL,
  `cantidad` VARCHAR(45) NULL,
  `precio_venta` VARCHAR(45) NULL,
  `prestado` TINYINT NULL,
  `Ventas_idVenta` INT NOT NULL,
  PRIMARY KEY (`idventas_detalle`),
  INDEX `fk_ventas_detalle_Garrafones1_idx` (`Garrafones_idGarrafon` ASC) VISIBLE,
  INDEX `fk_ventas_detalle_Ventas1_idx` (`Ventas_idVenta` ASC) VISIBLE,
  CONSTRAINT `fk_ventas_detalle_Garrafones1`
    FOREIGN KEY (`Garrafones_idGarrafon`)
    REFERENCES `aguazero`.`Garrafones` (`idGarrafon`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ventas_detalle_Ventas1`
    FOREIGN KEY (`Ventas_idVenta`)
    REFERENCES `aguazero`.`Ventas` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `aguazero`.`promociones_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`promociones_venta` (
  `idPromocionesVenta` INT NOT NULL AUTO_INCREMENT,
  `promociones_idpromocion` INT NOT NULL,
  `Ventas_idVentas` INT NOT NULL,
  PRIMARY KEY (`idPromocionesVenta`),
  INDEX `fk_promociones_venta_promociones1_idx` (`promociones_idpromocion` ASC) VISIBLE,
  INDEX `fk_promociones_venta_Ventas1_idx` (`Ventas_idVentas` ASC) VISIBLE,
  CONSTRAINT `fk_promociones_venta_promociones1`
    FOREIGN KEY (`promociones_idpromocion`)
    REFERENCES `aguazero`.`promociones` (`idpromocion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_promociones_venta_Ventas1`
    FOREIGN KEY (`Ventas_idVentas`)
    REFERENCES `aguazero`.`Ventas` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
