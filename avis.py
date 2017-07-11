vanishing_point = [[640.00366211, 419.82000732]]
# define source and destination targets
p1 = [vanishing_point[0] - width / 2, top]
p2 = [vanishing_point[0] + width / 2, top]
p3 = on_line(p2, vanishing_point, bottom)
p4 = on_line(p1, vanishing_point, bottom)
src_points = np.array([p1, p2, p3, p4], dtype=np.float32)
dst_points = np.array([[0, 0], [UNWARPED_SIZE[0], 0],
                       [UNWARPED_SIZE[0], UNWARPED_SIZE[1]],
                       [0, UNWARPED_SIZE[1]]], dtype=np.float32)
src = np.array([[353.00799561, 443.], [927., 443.],
                [3923.24804688, 685.], [-2643.24023438, 685.]], dtype=np.float32)
multi_lane_M = cv2.getPerspectiveTransform(src, dst_points)
one_lane_M = cv2.getPerspectiveTransform(src_points, dst_points)


def unwarp(img, m=M, size=ORIGINAL_SIZE):
    return cv2.warpPerspective(img, m, size, flags=cv2.WARP_FILL_OUTLIERS +
                                                   cv2.INTER_CUBIC + cv2.WARP_INVERSE_MAP)


def warp(img, m=M, size=ORIGINAL_SIZE):
    return cv2.warpPerspective(img, m, size)


polly = [-2.78294279e-04   2.89854798e-01   200]


def get_polly_line(polly_fit=polly, img):
    ploty = np.linspace(0, img.shape[0] - 1, img.shape[0])
    fitx = polly_fit[0] * ploty ** 2 + polly_fit[1] * ploty + polly_fit[2]
    return np.array([fitx, ploty], dtype=np.int32).T


def draw_warpped_lanes(shape=(720, 1280, 3), num=3, pad=200, polly=None):
    image = np.zeros(shape, dtype=np.uint8)
    lane_width = int((shape[1] - 2 * pad) / num)
    lanes = []
    if polly != None:
        lines = []
        draw_polly = polly
        for i in range(num):
            print(draw_polly)
            draw_polly[2] = pad + lane_width * i
            print(draw_polly)
            lines.append(get_polly_line(draw_polly, image))
        draw_polly[2] = pad + lane_width * num
        lines.append(get_polly_line(draw_polly, image))
        lines_img = draw_lines(image, lines)
        return ndimage.rotate(lines_img, 180), lines, draw_polly[2] / num

    else:
        for i in range(num):
            x_lane = pad + lane_width // 2 + i * lane_width
            lanes.append(x_lane)
            cv2.line(image, (int(x_lane - lane_width / 2), 0), (int(x_lane - lane_width / 2), shape[1]), (0, 0, 255),
                     10)
        cv2.line(image, (int(x_lane + lane_width / 2), 0), (int(x_lane + lane_width / 2), shape[1]), (0, 0, 255), 10)
        return image, lanes, lane_width