package io.github.jacobsims;
import robocode.*;
import robocode.util.Utils;
import java.awt.Color;

/**
 * AimingBot - a robot by Jacob
 */
public class AimingBot extends Robot
{
	/**
	 * run: AimingBot's default behavior
	 */
	public void run() {

		setColors(Color.black,Color.blue,Color.black);

		// Robot main loop
		while (true) {
			for (int i = 0; i < 10; i++) {
				ahead(99);
				turnGunRight(36);
				turnRight(36);
			}
			for (int i = 0; i < 10; i++) {
				ahead(99);
				turnGunLeft(36);
				turnLeft(36);
			}
		}
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		double bulletPower;
		if (e.getDistance() < 300) {
			bulletPower = 2;
		} else {
			bulletPower = 1;
		}

		double eBearingRelGun = Utils.normalRelativeAngleDegrees(e.getBearing() - (getGunHeading() - getHeading()));
		double currentPerpAxis = Math.sin(Math.toRadians(eBearingRelGun)) * e.getDistance();
		double currentHeadAxis = Math.cos(Math.toRadians(eBearingRelGun)) * e.getDistance();
		double eHeadingRelGun = Utils.normalRelativeAngleDegrees(e.getHeading() - (getGunHeading()));
		double projectedPerpAxis = 0;
		double projectedHeadAxis = 0;
		double projectionTime = (e.getDistance() / Rules.getBulletSpeed(bulletPower));
		for (int i=0; i < 10; i++) {
			projectedPerpAxis = currentPerpAxis + (Math.sin(Math.toRadians(eHeadingRelGun)) * e.getVelocity() * projectionTime);
			projectedHeadAxis = currentHeadAxis + (Math.cos(Math.toRadians(eHeadingRelGun)) * e.getVelocity() * projectionTime);
			projectionTime = Math.sqrt(projectedHeadAxis * projectedHeadAxis + projectedPerpAxis * projectedPerpAxis) / Rules.getBulletSpeed(bulletPower);
		}
		double angleToProjected = Math.toDegrees(Math.atan2(projectedPerpAxis, projectedHeadAxis));

		double gunTurnDegrees = angleToProjected;
		turnGunRight(gunTurnDegrees);

		fire(bulletPower);

		scan();
	}

	/**
	 * onHitByBullet: What to do when you're hit by a bullet
	 */
	public void onHitByBullet(HitByBulletEvent e) {
		// do nothing for now
	}

	/**
	 * onHitWall: What to do when you hit a wall
	 */
	public void onHitWall(HitWallEvent e) {
		// Replace the next line with any behavior you would like
		back(20);
		turnRight(40);
	}
}
