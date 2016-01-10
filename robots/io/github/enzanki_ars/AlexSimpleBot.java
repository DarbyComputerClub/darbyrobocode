package io.github.enzanki_ars;
import robocode.*;
import java.awt.Color;

// API help : http://robocode.sourceforge.net/docs/robocode/robocode/Robot.html

/**
 * DemoBot - a robot by Alex Shafer
 */
public class AlexSimpleBot extends AdvancedRobot
{
	private boolean cantSeeBot = true;
	
	public void run() {
		setColors(Color.green,Color.blue,Color.red);
		setAdjustGunForRobotTurn(true);
		while(true) {
			if (cantSeeBot) {
				setTurnGunLeft(10);
				setAhead(20);
			}
			else {
				cantSeeBot = true;
			}
			execute();
		}
	}

	public void onScannedRobot(ScannedRobotEvent e) {
		cantSeeBot = false;
		setTurnGunRight(0);
		setFire(2);
	}
	
	public void onHitByBullet(HitByBulletEvent e) {
		setBack(10);
		execute();
	}
	
	public void onHitRobot(HitRobotEvent e) {
		setBack(10);
		execute();
	}
	
	/**
	 * onHitWall: What to do when you hit a wall
	 */
	public void onHitWall(HitWallEvent e) {
		setBack(20);
		setTurnLeft(180);
		execute();
	}	
}
