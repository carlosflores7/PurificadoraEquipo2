-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema aguazero
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema aguazero
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `aguazero` DEFAULT CHARACTER SET utf8 ;
USE `aguazero` ;

-- -----------------------------------------------------
-- Table `aguazero`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`usuarios` (
  `idUsuario` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `correo` VARCHAR(45) NULL DEFAULT NULL,
  `password_hash` VARCHAR(256) NULL DEFAULT NULL,
  `tipo` VARCHAR(20) NULL DEFAULT NULL,
  `estatus` CHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY (`idUsuario`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`cliente` (
  `idCliente` INT(11) NOT NULL AUTO_INCREMENT,
  `domicilio` VARCHAR(45) NULL DEFAULT NULL,
  `localidad` VARCHAR(45) NULL DEFAULT NULL,
  `rfc` VARCHAR(15) NULL DEFAULT NULL,
  `Usuarios_idUsuario` INT(11) NOT NULL,
  PRIMARY KEY (`idCliente`),
  INDEX `fk_Cliente_Usuarios1_idx` (`Usuarios_idUsuario` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuario`)
    REFERENCES `aguazero`.`usuarios` (`idUsuario`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`puestos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`puestos` (
  `idPuesto` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `salario` INT(11) NULL DEFAULT NULL,
  `descripcion` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`idPuesto`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`empleado` (
  `idEmpleado` INT(11) NOT NULL AUTO_INCREMENT,
  `turno` VARCHAR(45) NOT NULL,
  `nss` VARCHAR(45) NOT NULL,
  `Usuarios_idUsuario` INT(11) NOT NULL,
  `puestos_idPuesto` INT(11) NOT NULL,
  `tipoEmpleado` CHAR(1) NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  UNIQUE INDEX `nss_UNIQUE` (`nss` ASC) VISIBLE,
  INDEX `fk_Empleado_Usuarios1_idx` (`Usuarios_idUsuario` ASC) VISIBLE,
  INDEX `fk_Empleado_puestos1_idx` (`puestos_idPuesto` ASC) VISIBLE,
  CONSTRAINT `fk_Empleado_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuario`)
    REFERENCES `aguazero`.`usuarios` (`idUsuario`),
  CONSTRAINT `fk_Empleado_puestos1`
    FOREIGN KEY (`puestos_idPuesto`)
    REFERENCES `aguazero`.`puestos` (`idPuesto`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`vehiculo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`vehiculo` (
  `idVehiculo` INT(11) NOT NULL AUTO_INCREMENT,
  `placas` VARCHAR(10) NULL DEFAULT NULL,
  `tipo_de_vehiculo` VARCHAR(45) NULL DEFAULT NULL,
  `tipo_combustible` VARCHAR(45) NULL DEFAULT NULL,
  `capacidad_tanque` VARCHAR(15) NULL DEFAULT NULL,
  `modelo` VARCHAR(45) NULL DEFAULT NULL,
  `a??o` CHAR(4) NULL DEFAULT NULL,
  `capacidad_garrafones` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idVehiculo`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`repartidor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`repartidor` (
  `idRepartidor` INT(11) NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT(11) NOT NULL,
  `Vehiculo_idVehiculo` INT(11) NOT NULL,
  `ruta` VARCHAR(45) NULL DEFAULT NULL,
  `folio_de_licencia` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idRepartidor`),
  INDEX `fk_Repartidor_Vehiculo1_idx` (`Vehiculo_idVehiculo` ASC) VISIBLE,
  INDEX `fk_Repartidor_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  CONSTRAINT `fk_Repartidor_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`empleado` (`idEmpleado`),
  CONSTRAINT `fk_Repartidor_Vehiculo1`
    FOREIGN KEY (`Vehiculo_idVehiculo`)
    REFERENCES `aguazero`.`vehiculo` (`idVehiculo`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`promociones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`promociones` (
  `idpromocion` INT(11) NOT NULL AUTO_INCREMENT,
  `estatus` TINYINT(4) NULL DEFAULT NULL,
  `porcentaje` DOUBLE NULL DEFAULT NULL,
  `codigo` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`idpromocion`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`pedidos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`pedidos` (
  `idPedido` INT(11) NOT NULL AUTO_INCREMENT,
  `cantidad_garrafones` INT(11) NOT NULL,
  `ClienteID` INT(11) NOT NULL,
  `idPromocion` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idPedido`),
  INDEX `FK_pedidos_cliente` (`ClienteID` ASC) VISIBLE,
  INDEX `FK_pedidos_promocion` (`idPromocion` ASC) VISIBLE,
  CONSTRAINT `FK_pedidos_cliente`
    FOREIGN KEY (`ClienteID`)
    REFERENCES `aguazero`.`cliente` (`idCliente`),
  CONSTRAINT `FK_pedidos_promocion`
    FOREIGN KEY (`idPromocion`)
    REFERENCES `aguazero`.`promociones` (`idpromocion`))
ENGINE = InnoDB
AUTO_INCREMENT = 81
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`ventas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`ventas` (
  `idVenta` INT(11) NOT NULL AUTO_INCREMENT,
  `precio_total` DOUBLE NULL DEFAULT NULL,
  `fecha` DATE NULL DEFAULT NULL,
  `estatus` VARCHAR(45) NULL DEFAULT NULL,
  `promociones_idpromocion` INT(11) NOT NULL,
  `Repartidor_idRepartidor` INT(11) NULL DEFAULT NULL,
  `idCliente` INT(11) NOT NULL,
  `idPedido` INT(11) NOT NULL,
  PRIMARY KEY (`idVenta`),
  INDEX `fk_Ventas_promociones1_idx` (`promociones_idpromocion` ASC) VISIBLE,
  INDEX `fk_Ventas_Repartidor1_idx` (`Repartidor_idRepartidor` ASC) VISIBLE,
  INDEX `fk_Ventas_idCliente_idx` (`idCliente` ASC) VISIBLE,
  INDEX `fk_Ventas_pedidos_idx` (`idPedido` ASC) VISIBLE,
  CONSTRAINT `fk_Ventas_Repartidor1`
    FOREIGN KEY (`Repartidor_idRepartidor`)
    REFERENCES `aguazero`.`repartidor` (`idRepartidor`),
  CONSTRAINT `fk_Ventas_idCliente`
    FOREIGN KEY (`idCliente`)
    REFERENCES `aguazero`.`cliente` (`idCliente`),
  CONSTRAINT `fk_Ventas_pedidos`
    FOREIGN KEY (`idPedido`)
    REFERENCES `aguazero`.`pedidos` (`idPedido`),
  CONSTRAINT `fk_Ventas_promociones1`
    FOREIGN KEY (`promociones_idpromocion`)
    REFERENCES `aguazero`.`promociones` (`idpromocion`))
ENGINE = InnoDB
AUTO_INCREMENT = 80
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`factura` (
  `idfactura` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha` VARCHAR(45) NULL DEFAULT NULL,
  `Cliente_idCliente` INT(11) NOT NULL,
  `Ventas_idVenta` INT(11) NOT NULL,
  PRIMARY KEY (`idfactura`),
  INDEX `fk_factura_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  INDEX `fk_factura_Ventas1_idx` (`Ventas_idVenta` ASC) VISIBLE,
  CONSTRAINT `fk_factura_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `aguazero`.`cliente` (`idCliente`),
  CONSTRAINT `fk_factura_Ventas1`
    FOREIGN KEY (`Ventas_idVenta`)
    REFERENCES `aguazero`.`ventas` (`idVenta`))
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`garrafones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`garrafones` (
  `idGarrafon` INT(11) NOT NULL AUTO_INCREMENT,
  `Estado` VARCHAR(15) NULL DEFAULT NULL,
  `codigo` CHAR(10) NULL DEFAULT NULL,
  `capaciodad` INT(11) NULL DEFAULT NULL,
  `precio_retornable` FLOAT NULL DEFAULT NULL,
  `precio_completo` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`idGarrafon`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`nominas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`nominas` (
  `idnomina` INT(11) NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT(10) UNSIGNED NOT NULL,
  `salario_total` DOUBLE NULL DEFAULT NULL,
  `dias_trabajados` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idnomina`),
  UNIQUE INDEX `Empleado_idEmpleado_UNIQUE` (`Empleado_idEmpleado` ASC) VISIBLE,
  INDEX `fk_nominas_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`tarjetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`tarjetas` (
  `idtarjeta` INT(11) NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT(11) NOT NULL,
  `numero_tarjeta` VARCHAR(45) NULL DEFAULT NULL,
  `banco` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idtarjeta`),
  UNIQUE INDEX `numero_tarjeta_UNIQUE` (`numero_tarjeta` ASC) VISIBLE,
  INDEX `fk_tarjetas_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  CONSTRAINT `fk_tarjetas_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`empleado` (`idEmpleado`))
ENGINE = InnoDB
AUTO_INCREMENT = 26
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`pagos` (
  `idPago` INT(11) NOT NULL AUTO_INCREMENT,
  `nominas_idnomina` INT(11) NOT NULL,
  `fecha` VARCHAR(45) NULL DEFAULT NULL,
  `tarjetas_idtarjeta` INT(11) NOT NULL,
  `dias_pe` VARCHAR(45) NOT NULL,
  `total` INT(11) NOT NULL,
  PRIMARY KEY (`idPago`),
  INDEX `fk_Pagos_nominas1_idx` (`nominas_idnomina` ASC) VISIBLE,
  INDEX `fk_Pagos_tarjetas1_idx` (`tarjetas_idtarjeta` ASC) VISIBLE,
  CONSTRAINT `fk_Pagos_nominas1`
    FOREIGN KEY (`nominas_idnomina`)
    REFERENCES `aguazero`.`nominas` (`idnomina`),
  CONSTRAINT `fk_Pagos_tarjetas1`
    FOREIGN KEY (`tarjetas_idtarjeta`)
    REFERENCES `aguazero`.`tarjetas` (`idtarjeta`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`prestamos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`prestamos` (
  `idPrestamos` INT(11) NOT NULL AUTO_INCREMENT,
  `Empleado_idEmpleado` INT(11) NULL DEFAULT NULL,
  `Ventas_idVentas` INT(11) NOT NULL,
  `Cliente_idCliente` INT(11) NOT NULL,
  `garrafones_prestados` INT(11) NOT NULL,
  `garrafones_entregados` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idPrestamos`),
  INDEX `fk_Prestamos_Empleado1_idx` (`Empleado_idEmpleado` ASC) VISIBLE,
  INDEX `fk_Prestamos_Ventas1_idx` (`Ventas_idVentas` ASC) VISIBLE,
  INDEX `fk_Prestamos_Cliente1_idx` (`Cliente_idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Prestamos_Cliente1`
    FOREIGN KEY (`Cliente_idCliente`)
    REFERENCES `aguazero`.`cliente` (`idCliente`),
  CONSTRAINT `fk_Prestamos_Empleado1`
    FOREIGN KEY (`Empleado_idEmpleado`)
    REFERENCES `aguazero`.`empleado` (`idEmpleado`),
  CONSTRAINT `fk_Prestamos_Ventas1`
    FOREIGN KEY (`Ventas_idVentas`)
    REFERENCES `aguazero`.`ventas` (`idVenta`))
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`promociones_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`promociones_venta` (
  `idPromocionesVenta` INT(11) NOT NULL AUTO_INCREMENT,
  `promociones_idpromocion` INT(11) NOT NULL,
  `Ventas_idVentas` INT(11) NOT NULL,
  PRIMARY KEY (`idPromocionesVenta`),
  INDEX `fk_promociones_venta_promociones1_idx` (`promociones_idpromocion` ASC) VISIBLE,
  INDEX `fk_promociones_venta_Ventas1_idx` (`Ventas_idVentas` ASC) VISIBLE,
  CONSTRAINT `fk_promociones_venta_Ventas1`
    FOREIGN KEY (`Ventas_idVentas`)
    REFERENCES `aguazero`.`ventas` (`idVenta`),
  CONSTRAINT `fk_promociones_venta_promociones1`
    FOREIGN KEY (`promociones_idpromocion`)
    REFERENCES `aguazero`.`promociones` (`idpromocion`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aguazero`.`ventas_detalle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `aguazero`.`ventas_detalle` (
  `idventas_detalle` INT(11) NOT NULL AUTO_INCREMENT,
  `Garrafones_idGarrafon` INT(11) NOT NULL,
  `cantidad` VARCHAR(45) NULL DEFAULT NULL,
  `precio_venta` VARCHAR(45) NULL DEFAULT NULL,
  `prestado` TINYINT(4) NULL DEFAULT NULL,
  `Ventas_idVenta` INT(11) NOT NULL,
  PRIMARY KEY (`idventas_detalle`),
  INDEX `fk_ventas_detalle_Garrafones1_idx` (`Garrafones_idGarrafon` ASC) VISIBLE,
  INDEX `fk_ventas_detalle_Ventas1_idx` (`Ventas_idVenta` ASC) VISIBLE,
  CONSTRAINT `fk_ventas_detalle_Garrafones1`
    FOREIGN KEY (`Garrafones_idGarrafon`)
    REFERENCES `aguazero`.`garrafones` (`idGarrafon`),
  CONSTRAINT `fk_ventas_detalle_Ventas1`
    FOREIGN KEY (`Ventas_idVenta`)
    REFERENCES `aguazero`.`ventas` (`idVenta`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

USE `aguazero` ;

-- -----------------------------------------------------
-- procedure sp_compraConfirmada
-- -----------------------------------------------------

DELIMITER $$
USE `aguazero`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compraConfirmada`(
	IN CODIGOPROMOCION CHAR(5),
    IN IDPEDIDOAUX INT,
    IN PRECIOTOTAL FLOAT,
    IN IDCLIENTE INT,
    IN GARRAFONES_PRESTADOS INT
)
BEGIN
	DECLARE IDPROMOCIONAUX INT;  
	DECLARE GARRAFONESAUX INT;
    DECLARE IDVENTAAUX INT;
    DECLARE FECHA date;
	
    SET IDPROMOCIONAUX = (SELECT IDPROMOCION FROM PROMOCIONES WHERE CODIGO = CODIGOPROMOCION);
    SET FECHA =(select CURDATE());
    
	#IF IDPROMOCIONAUX != "" THEN
	UPDATE PEDIDOS SET IDPROMOCION = IDPROMOCIONAUX WHERE IDPEDIDO = IDPEDIDOAUX; 
   
    SET GARRAFONESAUX = (SELECT CANTIDAD_GARRAFONES FROM PEDIDOS WHERE IDPEDIDO = IDPEDIDOAUX);
  
    INSERT INTO VENTAS (PRECIO_TOTAL,FECHA,ESTATUS,PROMOCIONES_IDPROMOCION,REPARTIDOR_IDREPARTIDOR,IDCLIENTE,IDPEDIDO) VALUES (PRECIOTOTAL, FECHA, "Sin asignar", IDPROMOCIONAUX, null, IDCLIENTE,IDPEDIDOAUX);
	
    SET IDVENTAAUX = (SELECT IDVENTA FROM VENTAS WHERE IDPEDIDO = IDPEDIDOAUX);
    
	IF (GARRAFONES_PRESTADOS != 0) THEN 
		INSERT INTO PRESTAMOS (EMPLEADO_IDEMPLEADO, VENTAS_IDVENTAS, CLIENTE_IDCLIENTE, GARRAFONES_PRESTADOS, GARRAFONES_ENTREGADOS) VALUES (null, IDVENTAAUX, IDCLIENTE, GARRAFONES_PRESTADOS,0);
	END IF;
    
    #ELSE 
		#SELECT MENSAJE "LA PROMOCION NO EXISTE";
    #END IF;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
