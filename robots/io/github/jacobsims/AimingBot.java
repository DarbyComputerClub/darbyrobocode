package io.github.jacobsims;
import robocode.*;
import robocode.util.Utils;
import java.awt.Color;
import java.util.Vector;

/**
 * AimingBot - a robot by Jacob
 */
public class AimingBot extends RateControlRobot
{
	private Vector<ScannedRobotEvent> recentScans;
	private boolean hadCollision;

	/**
	 * run: AimingBot's default behavior
	 */
	public void run() {
		recentScans = new Vector<ScannedRobotEvent>();
		hadCollision = false;

		setColors(Color.black,Color.blue,Color.black);
		setVelocityRate(Rules.MAX_VELOCITY);

		// Robot main loop
		while (true) {
			doMovement();
			setGunRotationRate(Rules.GUN_TURN_RATE);
			double firePower = 0;
			// Safe, because recentScans can only be updated during execute()
			for (ScannedRobotEvent e : recentScans) {
				double gunDiff = reactToRobotScan(e);
				double gunTurnAmount = gunDiff - getTurnRate();
				setGunRotationRate(gunTurnAmount);
				if (Math.abs(gunTurnAmount) < Rules.GUN_TURN_RATE) {
					firePower = bulletPowerForEvent(e);
				}
			}
			recentScans.clear();
			execute();
			if (firePower != 0) {
				setFire(firePower);
			}
		}
	}

	private double bulletPowerForEvent(ScannedRobotEvent e) {
		if (e.getDistance() < 300) {
			return 2;
		} else {
			return 1;
		}
	}

	private double reactToRobotScan(ScannedRobotEvent e) {
		double bulletPower = bulletPowerForEvent(e);

		double eBearingRelGun = Utils.normalRelativeAngleDegrees(e.getBearing() - (getGunHeading() - getHeading()));
		double currentPerpAxis = Math.sin(Math.toRadians(eBearingRelGun)) * e.getDistance();
		double currentHeadAxis = Math.cos(Math.toRadians(eBearingRelGun)) * e.getDistance();
		double eHeadingRelGun = Utils.normalAbsoluteAngleDegrees(e.getHeading() - (getGunHeading()));
		double projectedPerpAxis = 0;
		double projectedHeadAxis = 0;
		double projectionTime = (e.getDistance() / Rules.getBulletSpeed(bulletPower)) + 1;
		for (int i=0; i < 10; i++) {
			double addP = Math.sin(Math.toRadians(eHeadingRelGun)) * e.getVelocity() * projectionTime;
			double addH = Math.cos(Math.toRadians(eHeadingRelGun)) * e.getVelocity() * projectionTime;
			projectedPerpAxis = currentPerpAxis + addP;
			projectedHeadAxis = currentHeadAxis + addH;
			projectionTime = Math.sqrt(projectedHeadAxis * projectedHeadAxis + projectedPerpAxis * projectedPerpAxis) / Rules.getBulletSpeed(bulletPower) + 1;
		}
		double angleToProjected = Math.toDegrees(Math.atan2(projectedPerpAxis, projectedHeadAxis));

		// How much to turn the gun
		return angleToProjected;
	}

	public void doMovement() {
		// Stay off the edges
		double minX = 60;
		double minY = 60;
		double maxX = getBattleFieldWidth() - 60;
		double maxY = getBattleFieldHeight() - 60;
		if (getX() < minX) {
			setVelocityRate((getHeading() < 180 ? 1 : -1) * Rules.MAX_VELOCITY);
		} else if (getX() > maxX) {
			setVelocityRate((getHeading() < 180 ? -1 : 1) * Rules.MAX_VELOCITY);
		} else if (getY() < minY) {
			setVelocityRate((Math.abs(Utils.normalRelativeAngleDegrees(getHeading())) > 90 ? -1 : 1) * Rules.MAX_VELOCITY);
		} else if (getY() > maxY) {
			setVelocityRate((Math.abs(Utils.normalRelativeAngleDegrees(getHeading())) < 90 ? -1 : 1) * Rules.MAX_VELOCITY);
		}
		setTurnRate(getGoodTurnRate());
	}

	public double getGoodTurnRate() {
		double centerX = getBattleFieldWidth()/2;
		double centerY = getBattleFieldHeight()/2;
		double centerXRelX = centerX - getX();
		double centerYRelY = centerY - getY();
		double centerBearing = Utils.normalRelativeAngleDegrees(90 - Math.toDegrees(Math.atan2(centerYRelY, centerXRelX)));
		double centerBearingRelHeading = Utils.normalRelativeAngleDegrees(centerBearing - getHeading());
		if (getVelocity() == 0) {
			return 0;
		}
		double signModifier = getVelocity() / Math.abs(getVelocity());
		if (centerBearingRelHeading < 0) {
			return -Rules.MAX_TURN_RATE * signModifier;
		} else {
			return Rules.MAX_TURN_RATE * signModifier;
		}
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		recentScans.add(e);
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
		// Wall stuff should be taken care of by the bounds checking in doMovement
	}	

}
